import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';

export default class LobbyView extends Component {

  render() {
    const {onViewChanged} = this.props
    return (
      <div>
        <h1>Lobby</h1>
        <Button color="primary" variant="contained" onClick={onViewChanged}>Join Game</Button>
      </div>
    )
  }
}

LobbyView.propTypes = {
  onViewChanged: PropTypes.func,
}