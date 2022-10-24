import React, {useEffect, useState} from 'react'
import { useParams } from "react-router-dom"
import { Button, Container, Table } from '@mantine/core'
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { playerPageUrl, playerCreationUrl } from '../utils/urls'

function Players() {
    const params = useParams();
    const [players, setPlayers] = useState([])
    const [refreshTimer, setRefreshTimer] = useState(0)
    const navigate = useNavigate();

    useEffect(() => {
        getPlayers()
        setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
      }, [refreshTimer]);

    function getPlayers() {
        axios.get(playerCreationUrl(params.gameid))
        .then(function (response) {
          console.log(response);
          const temp = []
          for (let [id, player] of Object.entries(response.data.players)) {
              temp.push({'id': id, 'name': player.name, 'api':player.api})
          }
          console.log(temp)
          setPlayers(temp)
          console.log(players)
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayer(playerid) {
        axios.delete("/api" + playerPageUrl(params.gameid, playerid))
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayers() {
        axios.delete(playerCreationUrl(params.gameid))
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    return (
      <Container size="xl" px="sm">
        <h3>Players</h3>
        <Button variant="outline" color="red" radius="md" size="md" 
                onClick={() => withdrawPlayers()}>Withdraw All</Button>
        <hr/>

        <Table hover>
          <thead>
              <tr>
              <th>ID</th>
              <th>Name</th>
              <th>API</th>
              <th>ACTION</th>
              </tr>
          </thead>
          <tbody>
            { players.map(({name, api, id}) => (
              <tr key={id} onClick={() => navigate(id)}>
                <td>{id}</td>
                <td>{name}</td>
                <td>{api}</td>
                <td>
                  <Button variant="outline" color="red" radius="md" size="md" 
                    onClick={() => withdrawPlayer("./" + id)}>
                    Withdraw
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    )
  }

  export default Players
