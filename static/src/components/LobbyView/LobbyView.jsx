import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { FormControl } from '@material-ui/core';
import { Input } from '@material-ui/core';
import { InputLabel } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


export default class LobbyView extends Component {
  constructor(props) {
    super(props);
    this.state = { room: '', player: ''};
    this.joinGame = this.joinGame.bind(this)
    this.createGame = this.createGame.bind(this)
    this.updateRoom = this.updateRoom.bind(this)
    this.updatePlayer = this.updatePlayer.bind(this)
    this.handleResponse = this.handleResponse.bind(this)
  }

  joinGame(){
    const {socket} = this.props
    const {player, room} = this.state;
    socket.emit('join_game', {player:player, room:room}, (response) => this.handleResponse(response))
  }

  createGame(){
    const {socket} = this.props
    const {player, room} = this.state;
    socket.emit('create_game', {player:player, room:room}, (response) => this.handleResponse(response))
  }

  handleResponse(resp){
    if (resp.error){
        this.setState({error:resp.error})
    } else {
        this.setState({error:''})
    }
    //     const {onViewChanged} = this.props
    this.forceUpdate()
    //     const {onViewChanged} = this.props
  }

  updatePlayer(e) {
    const {room} = this.state;
    this.setState({player: e.target.value, room: room})
    this.forceUpdate()
  }

  updateRoom(e) {
    const {player} = this.state;
    this.setState({room: e.target.value, player: player})
    this.forceUpdate()
  }

  render() {
    const {error} = this.state
    return (
      <div className="lobby">

        <Grid
          container
          spacing={1}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '50vh' }}
        >
          <Grid item xs={3}>
            <Typography color="primary"><FontAwesomeIcon icon={["fas","hat-wizard"]} size="10x"/></Typography>
          </Grid>
          <Grid item xs={3}>
            <FormControl>
              <InputLabel htmlFor="player-input">Name</InputLabel>
              <Input id="player-input" onChange={this.updatePlayer}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <FormControl>
              <InputLabel htmlFor="room-input">Room</InputLabel>
              <Input id="room-input" onChange={this.updateRoom}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <Button color="primary" onClick={this.joinGame}>Join</Button>
            <Button color="primary" onClick={this.createGame}>Create</Button>
          </Grid>
          <Typography color="secondary">{error}</Typography>
        </Grid>
      </div>
    );
  }
}

LobbyView.propTypes = {
  onViewChanged: PropTypes.func,
  socket: PropTypes.any,
}