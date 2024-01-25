import { Component, Input } from '@angular/core';
import { ChatService, Conversation } from '../../services/chat.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-conversation-list',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './conversation-list.component.html',
  styleUrl: './conversation-list.component.scss'
})
export class ConversationListComponent {
  conversations$ = this._chatService.getConversations();
  constructor(private _chatService: ChatService) {}
  handleConversationSelection(conversation: Conversation) {
    this._chatService.setActiveConversation(conversation)
  }
}
