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
    this.state = { room: '', name: ''};
    this.onSubmit = this.onSubmit.bind(this)
    this.updateRoom = this.updateRoom.bind(this)
    this.updateName = this.updateName.bind(this)
  }

  onSubmit(){
    //     const {name, room} = this.state;
    const {onViewChanged} = this.props
    onViewChanged()
  }

  updateName(e) {
    const {room} = this.state;
    this.setState({name: e.target.value, room: room})
  }

  updateRoom(e) {
    const {name} = this.state;
    this.setState({room: e.target.value, name: name})
  }

  render() {
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
              <InputLabel htmlFor="name-input">Name</InputLabel>
              <Input id="name-input" onChange={this.updateName}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <FormControl>
              <InputLabel htmlFor="room-input">Room</InputLabel>
              <Input id="room-input" onChange={this.updateRoom}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <Button color="primary" onClick={this.onSubmit}>Join</Button>
            <Button color="primary" onClick={this.onSubmit}>Create</Button>
          </Grid>
        </Grid>
      </div>
    );
  }
}

LobbyView.propTypes = {
  onViewChanged: PropTypes.func,
}