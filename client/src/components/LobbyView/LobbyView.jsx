import React, { Component } from 'react';
import io from 'socket.io-client';
const socket = io('http://localhost:5000');

export default class Lobby extends Component {

    render() {
       const {onViewChanged} = this.props
       return (
       <div>
       <h1>Lobby</h1>
       <button type="button" onClick={onViewChanged}>Change View</button>
        </div>
       )
    }
}
