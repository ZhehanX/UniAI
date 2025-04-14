// src/utils/auth.js
export function getUserRole() {
    const token = localStorage.getItem('authToken');
    if (!token) return null;
    
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => 
        `%${('00' + c.charCodeAt(0).toString(16)).slice(-2)}`
      ).join(''));
      
      const payload = JSON.parse(jsonPayload);
      return payload.role || 'user'; // Adjust 'role' to match your JWT claim
    } catch (e) {
      console.error('Invalid token', e);
      return null;
    }
  }

export const getUserId = () => {
  const token = localStorage.getItem('authToken');
  if (!token) return null;
  
  try {
    // JWT tokens are in the format: header.payload.signature
    // We need to decode the payload part
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    const payload = JSON.parse(jsonPayload);
    return payload.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

export function isAuthenticated() {
    return !!localStorage.getItem('authToken');
}