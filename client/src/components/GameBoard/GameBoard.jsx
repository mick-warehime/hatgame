import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';

export default class GameBoard extends Component {
  constructor(props) {
    super(props);
    this.state = { counter: 0, timer: 0};
    this.addRandom = this.addRandom.bind(this);
    this.startTimer = this.startTimer.bind(this);
    this.incrementTimer = this.incrementTimer.bind(this);
  }

  componentDidMount () {
    const {socket} = this.props
    socket.on('increment_timer', this.incrementTimer)
  }

  incrementTimer() {
    const {timer} = this.state
    this.setState({ timer: timer + 1})
  }

  startTimer() {
    const {socket,} = this.props
    socket.emit("start_timer", {'duration': 5});
  }

  addRandom() {
    const {socket} = this.props
    const {counter} = this.state

    socket.emit("add_random", {'value':counter}, (resp) => this.setState({ counter: resp.value}) );
  }


  render() {
    const {counter} = this.state
    const {timer} = this.state
    return (
      <div>
        <h1>Count: {counter}</h1>
        <Button variant="contained" color="secondary" onClick={this.addRandom}>Add Something!</Button>
        <h1>Time: {timer}s</h1>
        <Button variant="contained" color="secondary" onClick={this.startTimer}>Toggle Timer</Button>
      </div>
    )
  }
}

GameBoard.propTypes = {
  socket: PropTypes.any,
}