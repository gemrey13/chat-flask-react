import { useState, useEffect } from 'react'
import Chatbox from './components/chatbox.jsx'
const baseUrl = 'http://127.0.0.1:5000/api/'
function App() {

  const [message, setMessage] = useState('');

  const handleChange = e => {
    console.log(`-----------${message}`);
    setMessage(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch(baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'content': message}),
    })
    if (response.ok) {
      console.log('Success')
      setMessage('')
    }
  }
  
  return (
    <>
      <div>      
      <Chatbox />
      
      <form onSubmit={handleSubmit}>
        <label htmlFor="content">Enter a message: </label>
        <input type="text" id="content" name="content" value={message} onChange={handleChange}/>
        <button type="submit">Send</button>
      </form>


      </div>
    </>
  )
}

export default App
