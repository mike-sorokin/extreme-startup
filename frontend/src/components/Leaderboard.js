import React from 'react'
import { useParams } from "react-router-dom"

function Leaderboard() {
  // const refresh = function() { window.location.reload() };
  // setTimeout(refresh, 10000);

  const params = useParams()

  return (
    <div>
      <title>Extreme Startup - Leaderboard</title>
      <body>
          <a href="/players">I want to play</a>
          <h1>Leaderboard</h1>
          {
            /* 
              <table>
                {% for player, score in leaderboard.items() %}
                    <tr>
                        <td>{{ player.name }}</td>
                        <td>{{ score }}</td>
                    </tr>
                {% endfor %}
              </table>
            */
          }
      </body>
      Leaderboard
    </div>
  )
}

export default Leaderboard