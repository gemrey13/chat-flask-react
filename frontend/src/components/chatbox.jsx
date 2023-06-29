import { useState, useEffect } from 'react'
import './chatbox.css';

// const baseUrl = 'http://127.0.0.1:5000/api/'
const baseUrl = 'https://gemreytest.pythonanywhere.com/api/'

function Chatbox() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchMessage = async () => {
      const respone = await fetch(baseUrl);
      let data = await respone.json();
      console.log(data.messages);
      setMessages(data.messages);
    };

    const intervalId = setInterval(fetchMessage, 2000);

    return () => {
      clearInterval(intervalId);
    };

  }, []);

  return (
    <>
      <div className='box'>
        {messages.map((message) => (
          <p key={message.id}>{message.content}</p>
        ))}
      </div>
    </>
  )
}

export default Chatbox
