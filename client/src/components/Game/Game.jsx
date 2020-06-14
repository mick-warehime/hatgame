import React, { Component } from 'react';
import io from 'socket.io-client';
const socket = io('http://localhost:5000')

export default class Game extends Component {
    constructor(props) {
      super(props);
      // intialize this.state.counter = 0
      this.state = { counter: 0, timer: 0 };
      this.addRandom = this.addRandom.bind(this);
      this.startTimer = this.startTimer.bind(this);
      this.incrementTimer = this.incrementTimer.bind(this);
    }

    componentDidMount () {
        // bind the incrementTimer message to the incrementTimer method
        socket.on('increment_timer', this.incrementTimer)
     }

    incrementTimer() {
        const {timer} = this.state
        this.setState({ timer: timer + 1 })
    }

    startTimer() {
        socket.emit("toggle_timer");
    }

    addRandom() {
        const {counter} = this.state
        socket.emit("add_random", {'value':counter}, resp => this.setState({ counter: resp.value }) );
    }


    render() {
       const {counter} = this.state
       const {timer} = this.state
       return (
       <div>
        <h1>Count: {counter}</h1>
        <button type="button" onClick={this.addRandom}>Add Something!</button>
        <h1>Time: {timer}s</h1>
        <button type="button" onClick={this.startTimer}>Toggle Timer</button>
        </div>
       )
    }
}
