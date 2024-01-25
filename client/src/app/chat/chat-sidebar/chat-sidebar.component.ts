import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { ChatService } from '../../services/chat.service';
import { ConversationListComponent } from '../conversation-list/conversation-list.component';

@Component({
  selector: 'app-chat-sidebar',
  standalone: true,
  imports: [
    ConversationListComponent
  ],
  templateUrl: './chat-sidebar.component.html',
  styleUrl: './chat-sidebar.component.scss'
})
export class ChatSidebarComponent implements OnInit {
  authInfo$ = this._authService.authState$;
  constructor(private _authService: AuthService, private router: Router, private _chatService: ChatService){}
  ngOnInit(): void {
    this.authInfo$.subscribe((info) => {
      console.log('Active AuthInfo - chat-sidebar')
      console.log(info)
      // Redirect if authenticated
      // if (info.user) {
      //   this.router.navigate(['/']); // Navigate to the protected page
      // }
    })
  }
  handleNewChat(): void {
    this._chatService.createConversation().subscribe();
  }
  signOut() {
    this._authService.signout().then(() => {
      this.router.navigate(['/signin']); // Navigate to the sign-in page
    });
  }

}
