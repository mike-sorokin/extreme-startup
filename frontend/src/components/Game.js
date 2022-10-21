import React from 'react'
import { Outlet, useParams } from "react-router-dom"
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'
import { useNavigate } from "react-router-dom";

function Game() {

  const params = useParams()
  const navigate = useNavigate();

  return (
    <>
    <Navbar collapseOnSelect bg="light" expand="lg" variant="light" activeKey="/leaderboard">
        <Container>
          <Navbar.Brand href="#home">Extreme Startup</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link onClick={() => navigate('/' + params.gameid + '/admin')}>Game</Nav.Link>
          </Nav>
          <Nav>
            <Nav.Link onClick={() => navigate('/' + params.gameid)}>Leaderboard</Nav.Link>
            <Nav.Link onClick={() => navigate('/' + params.gameid + '/players')}>Players</Nav.Link>
          </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    <Outlet />
    </>
  )
}

export default Game