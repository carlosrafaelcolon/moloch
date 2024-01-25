import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { UserMessageComponent } from '../messages/user-message/user-message.component';
import { AssistantMessageComponent } from '../messages/assistant-message/assistant-message.component';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
// import { Message } from '../../services/chat.service';
interface Message {
  role: 'user' | 'system' | 'assistant' | 'pending' | 'human' | 'ai';
  content: string;
}
@Component({
  selector: 'app-chat-list',
  standalone: true,
  imports: [
    CommonModule,
    UserMessageComponent,
    AssistantMessageComponent,
    MatProgressSpinnerModule
  ],
  templateUrl: './chat-list.component.html',
  styleUrl: './chat-list.component.scss'
})
export class ChatListComponent implements OnInit {
  @Input() messages: Message[] = [];
  ngOnInit(): void {
      
  }

}
