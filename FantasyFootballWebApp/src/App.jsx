import { useState, useEffect } from 'react'
import { Icon } from 'lucide-react';
import { football } from '@lucide/lab';
import './App.css'

function App() {
  const [userName, setUserName] = useState("")

  useEffect(() => {
    fetch("http://localhost:5000/")
    .then(res => res.text())
    .then(data => setUserName(data))
  }, [])

  return (
    <>
      <nav id="navbar">
        <div id="logoContainer">
          <Icon id="icon" iconNode={football}/>
          <div id="logoName">Fantasy Tracker</div>
        </div>
        <ul id="nav-links">
          <li><a>Home</a></li>
          <li><a>My Teams</a></li>
          <li><a>League Overview</a></li>
          <li><a>Standings</a></li>
        </ul>
      </nav>

      <div id="row">
        <div id="welcomeContainer">
          <h1>Welcome back,</h1>
          <h1>{userName || "Loading..."}</h1>
        </div>
        <div id="welcomeStats">
          <div id="statData">
            <h1></h1>
            <h1></h1>
          </div>
          <div id="statLabel">
            <h2>Projected</h2>
            <h2>Current</h2>
          </div>
        </div>
      </div>
      <div id="leagueStatsContainer">

      </div>
    </>
  )
}

export default App
