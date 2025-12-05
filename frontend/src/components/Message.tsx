import React from 'react'

interface MessageProps {
  type: 'success' | 'error'
  message: string
}

const Message: React.FC<MessageProps> = ({ type, message }) => {
  if (!message) return null

  return (
    <div className={`message ${type}`}>
      {message}
    </div>
  )
}

export default Message
