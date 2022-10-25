import { React, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Table } from "@mantine/core";

import { fetchPlayer } from "../utils/requests";

import PlayerEventCard from "./PlayerEventCard";

// TODO: fix playerDetail
function Player() {
  const [playerDetail, setPlayerDetail] = useState({})

  const params = useParams();

  useEffect(() => {
    const getPlayerData = async () => {
      try {
        const response = await fetchPlayer(params.gameid, params.id)
        setPlayerDetail(response)
      } catch (error) {
        // TODO
      }
    }

    getPlayerData()
  }, []);

  // function getPlayer() {
  //   axios.get("/api" + playerPageUrl(params.gameid, params.id))
  //     .then(function (response) {
  //       console.log(response);
  //       setPlayerDetail(response.data)
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  const sampleGameId = "asdaskmasom"
  const samplePlayerDetail = {
    id: "asonfaosmfi",
    game_id: "asdmasdasdasd",
    name: "John",
    api: "https://john.com",
    score: "1230"
  }

  return (
    <Container size="xl" px="xs">
      <br />
      <h3>Player ID</h3>
      <h4 style={{ color: 'grey' }}>{sampleGameId}</h4>
      <br />
      <h3>Game ID</h3>
      <h4 style={{ color: 'grey' }}>{samplePlayerDetail.game_id}</h4>
      <br />
      <h3>Name</h3>
      <h4 style={{ color: 'grey' }}>{samplePlayerDetail.name}</h4>
      <br />
      <h3>API</h3>
      <h4 style={{ color: 'grey' }}>{samplePlayerDetail.api}</h4>
      <br />
      <h3>Score</h3>
      <h4 style={{ color: 'grey' }}>{samplePlayerDetail.score}</h4>
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
  );
}

export default Player;
