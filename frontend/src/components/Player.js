import { React, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Container from "react-bootstrap/Container"
import Table from "react-bootstrap/Table"


import PlayerEventCard from "./PlayerEventCard";
import { playerPageUrl } from "../utils/urls";

// For testing only:
// const api = axios.create({
//   baseURL: "https://extreme-restartup.fly.dev/",
// });

function Player() {
  const params = useParams();
  const [playerDetail, setPlayerDetail] = useState({})
  

  useEffect(() => {
    getPlayer()
  }, []);

  function getPlayer(playerId) {
    axios.get(playerPageUrl(params.gameid, params.id))
        .then(function (response) {
          console.log(response);
          setPlayerDetail(response.data)
        })
        .catch(function (error) {
          console.log(error);
        });
  }



  return (
    <Container>
    <Container className="p-3">
      <br />
      <h3>Player ID</h3>
      <h4 style={{color: 'grey'}}>{params.id}</h4>
      <br />
      <h3>Game ID</h3>
      <h4 style={{color: 'grey'}}>{playerDetail.game_id}</h4>
      <br />
      <h3>Name</h3>
      <h4 style={{color: 'grey'}}>{playerDetail.name}</h4>
      <br />
      <h3>API</h3>
      <h4 style={{color: 'grey'}}>{playerDetail.api}</h4>
      <br />
      <h3>Score</h3>
      <h4 style={{color: 'grey'}}>{playerDetail.score}</h4>
      <br />
      <h3>Events</h3>
      <Table>
      <thead>
                <tr>
                <th>ID</th>
                <th>Query</th>
                <th>Difficulty</th>
                <th>Points</th>
                <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {/* {
                    playerDetail.events.map(({id, name, point}) => (
                        <tr>
                        <td>{id}</td>
                        <td>{name}</td>
                        <td>{point}</td>
                        </tr>
                    ))
                } */}
            </tbody>
      </Table>
    </Container>
    </Container>
  );
}

export default Player;
