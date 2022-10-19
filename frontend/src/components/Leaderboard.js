import React from 'react'
import { useParams } from "react-router-dom"

function Leaderboard() {
  // const refresh = function() { window.location.reload() };
  // setTimeout(refresh, 10000);

  const params = useParams()

  return (
    <div>
      <h2>Leaderboard</h2>
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
    </div>
  )
}

export default Leaderboard