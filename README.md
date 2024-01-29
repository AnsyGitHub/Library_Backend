# Community Library System Backend

Create a backend service for a community library system using FastAPI. This service manages books, members, and borrowing records, and implements user authentication for secure access.

## Authentication

Implement user authentication using FastAPI's security utilities:

- Users can sign up, log in, and log out.
- JWT tokens are used to manage sessions and secure endpoints.

## Database Models

Define the following database models:

### Book

Holds information about books such as title, author, and ISBN.

### Member

Stores member details including name, email, and membership ID.

### BorrowRecord

Records the details when a member borrows a book, including borrow date and return date.

## Relationships

Establish relationships between models:

- A Member can borrow multiple Books.
- A Book can be borrowed by multiple Members (not simultaneously).
- BorrowRecord joins Books and Members to keep track of who borrowed what and when.

## Endpoints

Implement the following endpoints:

### Authentication Endpoints

- Sign up
- Login
- Logout

### CRUD Operations

For Books and Members:

- Create
- Read
- Update
- Delete

### View Borrowed Books

- View all the books a member has borrowed (past and present).

### View Borrowing Members

- View all members who have borrowed a particular book.