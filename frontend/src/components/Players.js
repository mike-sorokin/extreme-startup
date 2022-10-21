import Container from 'react-bootstrap/Container'
import React, {useEffect, useState} from 'react'
import { useParams } from "react-router-dom"
import Button from 'react-bootstrap/Button'
import Stack from 'react-bootstrap/Stack'
import Table from 'react-bootstrap/Table'
import axios from 'axios'
import { requestGameCreation } from '../utils/requests'

function Players() {
    const params = useParams();
    const [players, setPlayers] = useState([])
    const [refreshTimer, setRefreshTimer] = useState(0)

    useEffect(() => {
        getPlayers()
        setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
      }, [refreshTimer]);

    function getPlayers() {
        axios.get("http://127.0.0.1:5000/api/" + params.gameid + '/players')
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
        axios.delete("http://127.0.0.1:5000/api/" + params.gameid + '/players/' + playerid)
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayers() {
        axios.delete("http://127.0.0.1:5000/api/" + params.gameid + '/players')
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  
    return (
      <Container className="p-5">
          <Stack direction="horizontal" gap={2}>
            <Stack>
                <h3>Players</h3>
            </Stack>
            <Button variant="outline-primary">Add Player</Button>
            <Button variant="outline-danger" onClick={() => withdrawPlayers()}>Withdraw All</Button>
          </Stack>
          <hr/>

          <Table>
            <thead>
                <tr>
                <th>ID</th>
                <th>Name</th>
                <th>API</th>
                <th>ACTION</th>
                </tr>
            </thead>
            <tbody>
                {
                    players.map(({name, api, id}) => (
                        <tr>
                        <td>{id}</td>
                        <td>{name}</td>
                        <td>{api}</td>
                        <td><Button variant="outline-danger" onClick={() => withdrawPlayer(id)}>Withdraw</Button></td>
                        </tr>
                    ))
                }
            </tbody>
            </Table>
      </Container>
    )
  }

  export default Players