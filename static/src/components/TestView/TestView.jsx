import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';

export default class TestView extends Component {
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
    const {socket} = this.props
    socket.emit("start_timer", {'duration': 5});
  }

  addRandom() {
    const {socket} = this.props
    const {counter} = this.state

    socket.emit("add_random", {'value':counter}, (resp) => this.setState({ counter: resp.value}) );
  }


  render() {
    const {counter, timer} = this.state;
    const {boardViewChanged} = this.props;
    return (
      <div>
        <h1>Count: {counter}</h1>
        <Button variant="outlined" color="secondary" onClick={this.addRandom}>Add Something!</Button>
        <h1>Time: {timer}s</h1>
        <Button variant="outlined" color="secondary" onClick={this.startTimer}>Toggle Timer</Button>
        <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.PHRASE)}>PHRASE</Button>
      </div>
    )
  }
}

TestView.propTypes = {
  socket: PropTypes.any,
  boardViewChanged: PropTypes.func,
}