import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import { List } from '@material-ui/core';
import { ListItem } from '@material-ui/core';
import { ListItemText } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

export default class GameStatus extends Component {
  constructor(props) {
    super(props);
    this.state = { team1: [], score1: 0, icon1: "hat-wizard",
      team2: [], score2: 0, icon2: "hat-wizard"};
    this.teamList = this.teamList.bind(this)
    this.updateStatus = this.updateStatus.bind(this)
  }

  componentDidMount () {
    const {socket} = this.props
    socket.on('update_status', (response) => {this.updateStatus(response);});
    socket.emit('get_status');
  }

  updateStatus(resp) {
    this.setState({team1: resp["team1"], score1:resp["score1"], icon1:resp["icon1"],
      team2: resp["team2"], score2:resp["score2"], icon2:resp["icon2"]})
    this.forceUpdate();
  }

  teamList(names, icon, score, color) {
    const iconValue = ["fas", 'american-sign-language-interpreting']
    return (<List dense={true}>
      <ListItem key='icon' divider={true}>
        <Typography color={color}><FontAwesomeIcon icon={iconValue} size="3x"/></Typography>
      </ListItem>
      <ListItem key='score' divider={true}>
        <Typography color={color} style={{ fontSize: 50 }}>{score}</Typography>
      </ListItem>
      {names.map((name) => (<ListItem key={name} divider={true}><ListItemText primary={name}/> </ListItem>))}
    </List>);
  }

  render() {

    const {onViewChanged} = this.props
    const {team1,icon1,score1,team2,icon2,score2} = this.state
    return (
      <div>
        <Grid container spacing={0}>
          <Grid item xs={6}>
            {this.teamList(team1, icon1, score1, "primary")}
          </Grid>
          <Grid item xs={6}>
            {this.teamList(team2, icon2, score2, "secondary")}
          </Grid>
          <Grid item xs={12}>
            <Button color="primary" >Randomize Teams</Button>
          </Grid>
          <Grid item xs={12}>
            <Button color="primary" onClick={onViewChanged}>Leave</Button>
          </Grid>
          <Grid item xs={12}>
            <Button color="primary" variant="contained">Start</Button>
          </Grid>
        </Grid>
      </div>
    )
  }
}

GameStatus.propTypes = {
  onViewChanged: PropTypes.func,
  socket: PropTypes.any,
}
