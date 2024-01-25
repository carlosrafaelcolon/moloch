import { Component, OnInit } from '@angular/core';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import { ChatListComponent } from '../chat-list/chat-list.component';
import { ChatService, Message } from '../../services/chat.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat-panel',
  standalone: true,
  imports: [
    ChatListComponent,
    ChatInputComponent,
    CommonModule
  ],
  templateUrl: './chat-panel.component.html',
  styleUrl: './chat-panel.component.scss'
})
export class ChatPanelComponent implements OnInit {
  activeConversation$ = this._chatService.getActiveConversation();

  constructor(private _chatService: ChatService) { }
  ngOnInit(): void {

    this._chatService.fetchConversations().subscribe(conversations => {
      if (conversations.length === 0) {
        this._chatService.createConversation().subscribe();
      }
    });
  }

  handleSubmit(messageContent: string) {
    if (messageContent) {
      const message: Message = {
        content: messageContent,
        role: 'user',
        // You may add other properties if needed, like id
      };
      console.log(message)
      this._chatService.sendStreamingMessage(message);
    }
  }

}
