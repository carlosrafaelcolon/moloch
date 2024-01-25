import { Routes } from '@angular/router';
import { ChatComponent } from './chat/chat.component';
import { SigninComponent } from './auth/signin/signin.component';
import { authGuard } from './services/auth.guard';

export const routes: Routes = [
    {path:'signin', component: SigninComponent},
    {
        path: '', 
        component: ChatComponent,
        canActivate: [authGuard]
    },
    
];
