import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-signin',
  standalone: true,
  imports: [
    ReactiveFormsModule 
  ],
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.scss'
})
export class SigninComponent implements OnInit, OnDestroy {
  signinForm!: FormGroup;
  authInfo$ = this._authService.authState$;
  private authSubscription!: Subscription;
  constructor(
    private _fb:FormBuilder, 
    private _authService: AuthService,
    private router: Router
    ) {}
  ngOnInit() {
    this.signinForm = this._fb.group({
      email: ['user@example.com', [Validators.required, Validators.email]],
      password: ['mypassword', [Validators.required]]
    });
    this.authSubscription = this.authInfo$.subscribe((info) => {
      console.log('Active AuthInfo')
      console.log(info)
      if (info.user) {
        this.router.navigate(['/']); // Navigate to the protected page
        this.authSubscription.unsubscribe(); // Unsubscribe to stop further execution
      }
    });
  
    // this.authInfo$.subscribe((info) => {
    //   console.log('Active AuthInfo')
    //   console.log(info)
    //   // Redirect if authenticated
    //   if (info.user) {
    //     this.router.navigate(['/']); // Navigate to the protected page
    //   }
    // })
  }
  async onSubmit() {
    if (this.signinForm.valid) {
      console.log(this.signinForm.value);
      const { email, password } = this.signinForm.value;
      await this._authService.signin(email, password);
    }
  }
  ngOnDestroy() {
    if (this.authSubscription) {
      this.authSubscription.unsubscribe();
    }
  }
}
