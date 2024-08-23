import { NgFor } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { map } from 'rxjs/operators';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgFor, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  allUsers: any = [];

  private API_URL = 'http://localhost:8000/';

  constructor(private http: HttpClient) {
    this.getIsueByRepository();
  }

  ngOnInit(): void {
    // this.getIsueByRepository();
  }

  getIsueByRepository() {
    this.http.get(this.API_URL + 'user-all')
      .subscribe((res: any) => {
        this.allUsers = res;
        
      })
  }
}
