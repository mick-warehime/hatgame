import React, { Component } from 'react';
import { Views } from '../../utils/constants';
import LobbyView from '../LobbyView/LobbyView';
import GameView from '../GameView/GameView';

// The socket controls all the interactions with the backend.
// To 'call' the backend
// socket.emit('foo', request, (response) => {callback(response)}

// To listen to message from the backend
// socket.on('bar', (response) => {callback(response})
import io from 'socket.io-client';
const socket = io();

export default class Controller extends Component {
  constructor(props) {
    super(props);
    this.state = {view: Views.LOBBY}
    this.changeViewTo = this.changeViewTo.bind(this)
  }

  changeViewTo(newView) {
    const {view} = this.state
    var newView = Views.LOBBY
    if (view == Views.LOBBY){
      newView = Views.GAME
    }
    this.setState({view: newView})
  }

  render() {
    const {view} = this.state;
    switch (view) {
    case Views.LOBBY:
      return <LobbyView changeViewTo={this.changeViewTo} socket={socket}/>;
    case Views.GAME:
      return  <GameView changeViewTo={this.changeViewTo} socket={socket}/>;
    default:
      return (
        <div>
          <h1>Sorry not implemented</h1>
        </div>
      )
    }
  }
}