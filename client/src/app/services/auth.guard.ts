import { ActivatedRouteSnapshot, RouterStateSnapshot, CanActivateFn, Router } from '@angular/router';
import {  inject } from '@angular/core';
import { AuthService } from './auth.service'; // Adjust the import path as needed
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';



export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
): Observable<boolean> => {
  console.log('auth guard activated!!!!')
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.checkSession().pipe(
    map(user => {
      if (user) {
        console.log("user existed so page allowed")
        // User is authenticated
        return true;
      } else {
        console.log('redirect to /signin')
        // User is not authenticated, redirect to login
        router.navigate(['/signin']);
        return false;
      }
    }),
    catchError(() => {
      console.log('ERRORRRRRRRR - redirect to /signin')
      // Handle error, redirect to login
      router.navigate(['/signin']);
      return of(false);
    })
  );
};