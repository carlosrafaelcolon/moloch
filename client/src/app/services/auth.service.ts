import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, firstValueFrom, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';

export type User = {
  id: string;
  email: string;
} | any;
// null | false
export interface AuthInfo {
  user: User;
  error: string;
  loading: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private baseUrl = '/api/auth';
  private authSubject = new BehaviorSubject<AuthInfo>({ user: null, error: '', loading: false });
  constructor(private http: HttpClient) { }

  get authState$(): Observable<AuthInfo> {
    return this.authSubject.asObservable();
  }

  async signin(email: string, password: string): Promise<void> {
    this.updateState({ error: '', loading: true });
    try {
      const data = await firstValueFrom(this.http.post<User>(`${this.baseUrl}/signin`, { email, password }));
      this.updateState({ user: data, error: '' });
    } catch (error) {
      this.updateState({ error: 'Error Message', loading: false });
    }
  }

  async signout(): Promise<void> {
    this.updateState({ loading: true });
    try {
      await firstValueFrom(this.http.post(`${this.baseUrl}/signout`, {}));
      this.updateState({ user: null, error: '', loading: false });
    } catch (error) {
      this.updateState({ error: 'Error Message', loading: false });
    }
  }

  // Method to check the user session
  // checkSession(): Observable<User> {
  //   return this.http.get<User>(`${this.baseUrl}/user`);
  // }
  // checkSession(): Observable<User> {
  //   this.updateState({ loading: true });
  //   return this.http.get<User>(`${this.baseUrl}/user`).pipe(
  //     map(user => {
  //       this.updateState({ user, loading: false });
  //       return user || false; // Ensure the return value is of type User
  //     }),
  //     catchError(error => {
  //       this.updateState({ user: false, error: 'Failed to fetch user', loading: false });
  //       return of(false); // `of(false)` is of type Observable<false>, which aligns with Observable<User>
  //     })
  //   );
  // }
  checkSession(): Observable<User> {
    this.updateState({ loading: true });
    return this.http.get<User>(`${this.baseUrl}/user`).pipe(
      map(user => {
        this.updateState({ user, loading: false });
        // Explicitly cast the return type to align with 'User'
        return (user !== null ? user : false) as User;
      }),
      catchError(error => {
        this.updateState({ user: false, error: 'Failed to fetch user', loading: false });
        // Explicitly cast the return type to align with 'User'
        return of(false as User);
      })
    );
  }

  // checkSession(): Observable<User> {
  //   this.updateState({ loading: true });
  //   return this.http.get<User>(`${this.baseUrl}/user`).pipe(
  //     map(user => {
  //       this.updateState({ user, loading: false });
  //       return user !== null ? user : false; // Ensures that 'user' is of type User
  //     }),
  //     catchError(error => {
  //       this.updateState({ user: false, error: 'Failed to fetch user', loading: false });
  //       return of(false); // Returning Observable<false>, which aligns with Observable<User>
  //     })
  //   );
  // }

  private updateState(newState: Partial<AuthInfo>): void {
    this.authSubject.next({ ...this.authSubject.value, ...newState });
  }
}
