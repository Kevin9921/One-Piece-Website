import React, {useEffect, useState} from 'react'

function App() {
  const [backendData, setBackendData] = useState([{}])

  useEffect(() => {
    fetch("/api").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, [])
  return (
    <div>
      {(typeof backendData === 'undefined') ? (
        <p>Loading...</p>
      ):(backendData.map((row, i) => (
        <div key={i}>
          <p>Character ID: {row.character_id}</p>
          <p>Name: {row.name}</p>
          <img src={row.image_url} alt={row.name} style={{ maxWidth: '100px', maxHeight: '100px' }} />
        </div>
      ))
    )
      }
    </div>
  )
}

export default App