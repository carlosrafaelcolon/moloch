import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { Injectable } from '@angular/core';

export interface Message {
  id?: number | string;
  role: 'user' | 'assistant' | 'system' | 'pending';
  content: string;
}

export interface Conversation {
  id: number;
  messages: Message[];
}

export interface MessageOpts {
  useStreaming?: boolean;
  documentId?: string;
}

export interface ChatState {
  error: string;
  loading: boolean;
  activeConversationId: number | null;
  conversations: Conversation[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private baseUrl = '/api/conversations';
  private activeConversation = new BehaviorSubject<Conversation | null>(null);
  private conversations = new BehaviorSubject<Conversation[]>([]);
  private errorSubject = new BehaviorSubject<string>('');

  constructor(private http: HttpClient) { }
  // conversations
  getActiveConversation(): Observable<Conversation | null> {
    return this.activeConversation.asObservable();
  }
  getConversations(): Observable<Conversation[]> {
    return this.conversations.asObservable();
  }



  fetchConversations(): Observable<Conversation[]> {
    return this.http.get<Conversation[]>(this.baseUrl)
      .pipe(
        tap(conversations => {
          this.conversations.next(conversations); 
          if (conversations && conversations.length > 0) {
            this.setActiveConversation(conversations[0]);
          }
        }),
        catchError((error) => this.handleError(error))
      );
  }

  createConversation(): Observable<Conversation> {
    return this.http.post<Conversation>(this.baseUrl, {})
      .pipe(
        tap(newConversation => {
          this.setActiveConversation(newConversation);
          this.addConversation(newConversation);
        }),
        catchError((error) => this.handleError(error))
      );
  }
  private addConversation(conversation: Conversation) {
    const currentConversations = this.conversations.getValue();
    this.conversations.next([...currentConversations, conversation]);
  }

  setActiveConversation(conversation: Conversation): void {
    this.activeConversation.next(conversation);
  }
  // messages
  sendStreamingMessage(message: Message) {
    const activeConversation = this.activeConversation.getValue();

    if (!activeConversation) {
      console.error('No active conversation');
      return;
    }

    // Append the user message to the active conversation
    this.appendMessageToActiveConversation(message);
    // Placeholder for a response message that indicates loading/pending state
    const responseMessage: Message = {
      role: 'pending',
      content: '',
      id: Date.now().toString(36) + Math.random().toString(36) // Generate a unique id for the response message
    };
    // Append the placeholder response message
    this.appendMessageToActiveConversation(responseMessage);


    // Use Fetch API for streaming
    fetch(`${this.baseUrl}/${activeConversation.id}/messages?stream=true`, {
      method: 'POST',
      body: JSON.stringify({ input: message.content }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        } else {
          return response.body;
        }
      })
      .then(stream => {
        if (stream) {
          this.readResponse(stream, responseMessage.id);
        }
      })
      .catch(error => {
        console.error('Error during streaming:', error);
        this.errorSubject.next('Error during streaming');
      });


  }
  // // Send the user's message to the server
  // this.http.post<any>(`${this.baseUrl}/${activeConversation.id}/messages?stream=true`, {
  //   input: message.content
  // }, { responseType: 'json' })
  //   .pipe(
  //     catchError((error) => this.handleError(error))
  //   )
  //   .subscribe({
  //     next: (response) => {
  //       // Handle the streaming response here
  //       // Assuming the server sends a continuous stream of data
  //       if (response.stream && responseMessage.id) {
  //         this.readResponse(response.stream, responseMessage.id);
  //       }
  //     },
  //     error: (error) => {
  //       // Handle any errors that occur during the request
  //       console.error('Error during streaming:', error);
  //       this.errorSubject.next('Error during streaming');

  //     }
  //   });
  private appendMessageToActiveConversation(message: Message) {
    const currentConversation = this.activeConversation.getValue();

    if (currentConversation) {
      const updatedMessages = [...currentConversation.messages, message];
      const updatedConversation = { ...currentConversation, messages: updatedMessages };
      this.activeConversation.next(updatedConversation);
    }
  }

  private readResponse(stream: ReadableStream<Uint8Array>, responseMessageId: any) {
    const reader = stream.getReader();
    let inProgress = true;

    const processChunk = async () => {
      while (inProgress) {
        const { done, value } = await reader.read();


        if (done) {
          inProgress = false;

          this.finalizeResponseMessage(responseMessageId);
          break;
        }

        const text = new TextDecoder().decode(value);
        this.appendResponseTextToMessage(responseMessageId, text);
      }
    };

    processChunk().catch(err => {
      console.error('Error while reading response:', err);
      this.errorSubject.next('Error while reading response');
    });
  }

  // New method to finalize the message
  private finalizeResponseMessage(responseMessageId: any) {
    const currentConversation = this.activeConversation.getValue();

    if (currentConversation) {
      const updatedMessages = currentConversation.messages.map(message => {
        if (message.id === responseMessageId) {
          return { ...message, role: 'assistant' as const }; // Change role to 'assistant'
        }
        return message;
      });

      const updatedConversation = { ...currentConversation, messages: updatedMessages };
      this.activeConversation.next(updatedConversation);
    }
  }
  private appendResponseTextToMessage(responseMessageId: any, text: string) {
    const currentConversation = this.activeConversation.getValue();

    if (currentConversation) {
      const updatedMessages = currentConversation.messages.map(message => {
        if (message.id === responseMessageId) {
          // Explicitly type 'role' as 'assistant'
          return { ...message, content: message.content + text, role: 'assistant' as const };
        }
        return message;
      });

      const updatedConversation = { ...currentConversation, messages: updatedMessages };
      this.activeConversation.next(updatedConversation);
    }
  }

  private removeMessageFromActive(messageId: any) {
    console.log('ENTERING removeMessageFromActive')
    const currentConversation = this.activeConversation.getValue();
    console.log('currentConversation  ----------------------------------')
    console.log(currentConversation)

    if (currentConversation) {
      const updatedMessages = currentConversation.messages.filter(m => {
        return m.id !== messageId
      });
      console.log('updated messaged ---------------------------------')
      console.log(updatedMessages)
      const updatedConversation = { ...currentConversation, messages: updatedMessages };
      console.log('updatedConversation ----------------------------------')
      console.log(updatedConversation)
      this.activeConversation.next(updatedConversation);

    }
    console.log('LEAVING removeMessageFromActive')
  }
  getError(): Observable<string> {
    return this.errorSubject.asObservable();
  }
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Something went wrong';
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    this.errorSubject.next(errorMessage);
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
