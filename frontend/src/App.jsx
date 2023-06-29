import { useState, useEffect } from 'react'

const baseUrl = 'http://127.0.0.1:5000/api/'

function App() {
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
      <div>
      {messages.map((message) => (
        <p key={message.id}>{message.content}</p>
      ))}
      

      <form action="">
        <label htmlFor="content">Enter a message: </label>
        <input type="text" id="content" />
        <button type="submit">Send</button>
      </form>
      </div>
    </>
  )
}

export default App
