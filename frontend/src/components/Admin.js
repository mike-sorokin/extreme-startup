import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Button, Container } from "@mantine/core";
import axios from "axios";

import { fetchGame, updateGame } from "../utils/requests";
import { gameUrl } from "../utils/urls";

import "../styles/Admin.css";

function Admin() {
  const [playerNo, setPlayerNo] = useState(0);
  // Removing round 0 = "Warmup" and just keeping it to 0
  // It is implied that round 0 is the warmup round
  // Change it manually in frontend if you need to display warmup
  const [round, setRound] = useState(0);
  const [refreshTimer, setRefreshTimer] = useState(0);

  const params = useParams();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetchGame(params.gameId);
        setRound(response.round);
        setPlayerNo(response.players.length);
      } catch (error) {
        // TODO
      }
    };

    fetchData();

    // What is this for?
    setTimeout(() => setRefreshTimer((prevState) => prevState + 1), 1000);
  }, []);

  // useEffect(() => {
  //   axios
  //     .get(gameUrl(params.gameid))
  //     .then(function (response) {
  //       console.log(response);
  //       setRound(response.data.round === 0 ? "Warmup" : response.data.round);
  //       setPlayerNo(response.data.players.length);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });

  //   setTimeout(() => setRefreshTimer((prevState) => prevState + 1), 1000);
  // }, [refreshTimer]);

  const advanceRound = async () => {
    const response = await updateGame(params.gameid, { round: round + 1 });

    if (response) {
      setRound(round + 1);
    }
  };
  // function advanceRound() {
  //   axios
  //     .put(gameUrl(params.gameid))
  //     .then(function (response) {
  //       console.log(response);
  //       setRound(round === "Warmup" ? 1 : round + 1);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  // const roundsBarStyle = {
  //   width: "100%",
  //   display: "inline-flex",
  //   flexDirection: "row",
  //   justifyContent: "space-between",
  //   alignItems: "center",
  // };

  return (
    <Container size="xl" px="xs">
      <h3>Game ID</h3>
      <h4 className="bar">{params.gameid}</h4>
      <br />
      <h3>Number of Players</h3>
      <h4 className="bar">{playerNo}</h4>
      <br />
      <div className="roundsBar">
        <div>
          <h3>Rounds</h3>
        </div>
        <Button
          variant="outline"
          color="dark"
          radius="md"
          size="md"
          style={{
            marginLeft: "20px",
          }}
          onClick={() => advanceRound()}
        >
          Advance Round
        </Button>
      </div>
      <h4 className="bar">{round}</h4>
    </Container>
  );
}

export default Admin;
