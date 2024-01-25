import { Component, OnInit } from '@angular/core';
import {CommonModule} from '@angular/common'
import { ChatSidebarComponent } from './chat-sidebar/chat-sidebar.component';
import { ChatPanelComponent } from './chat-panel/chat-panel.component';
import { ChatService } from '../services/chat.service';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import { ConversationListComponent } from './conversation-list/conversation-list.component';
import {MatButtonModule} from '@angular/material/button';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    ChatSidebarComponent,
    ChatPanelComponent,
    ConversationListComponent,
    MatSidenavModule,
    MatIconModule,
    MatButtonModule
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent implements OnInit {
  sidebarVisible = true; // Initially visible
  activeConversation$ = this._chatService.getActiveConversation();
  authState$ = this._authService.authState$;
  error$ = this._chatService.getError();
  // useStreaming: boolean = !!localStorage.getItem('streaming');
  constructor(private _chatService: ChatService, private _authService: AuthService, private router: Router) {}

  toggleSidebar() {
    this.sidebarVisible = !this.sidebarVisible;
    console.log("Sidebar state", this.sidebarVisible)
  }
  ngOnInit(): void {
 
      // this.activeConversation$.subscribe((convo) => {
      //   console.log('Active Conversation in Chat')
      //   console.log(convo)
      // })
  }
  handleNewChat(): void {
    this._chatService.createConversation().subscribe();
  }
  handleSubmit(text: string): void {
    // Implement submit logic
  }
  signOut() {
    this._authService.signout().then(() => {
      this.router.navigate(['/signin']); // Navigate to the sign-in page
    });
  }
  toggleStreaming(): void {
    // this.useStreaming = !this.useStreaming;
    // localStorage.setItem('streaming', this.useStreaming ? 'true' : '');
  }

}


