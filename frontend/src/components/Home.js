import React from 'react'

function Home() {

  // const [name, setName] = useState("")
  // const [url, setUrl] = useState("")

  return (
    <div className="Home">
    <h1>Add a new player</h1>
      <form method="post" action="https://extreme-restartup.fly.dev/players">
          <label htmlFor="name">Name: </label>
          <input type="text" id="name" name="name"/>

          <label htmlFor="url">URL: </label>
          <input type="text" id="url" name="url" placeholder="http://...."/>

          <input type="submit" value="Submit" />
      </form>
  </div>
  )
}

export default Home
