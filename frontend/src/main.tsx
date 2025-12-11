import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'


createRoot(document.getElementById('root')!).render(
  
    <BrowserRouter>
      <StrictMode>
        <GoogleOAuthProvider clientId='85018584806-eph12bspmbel76f31p44k5qd7vej02mo.apps.googleusercontent.com'>
          <App />
        </GoogleOAuthProvider>
      </StrictMode>
    </BrowserRouter>
  
  ,
)
