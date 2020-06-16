import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';

export default class GameStatus extends Component {
  render() {
    const {onViewChanged} = this.props
    return (
      <div>
        <h1>Game</h1>
        <Button variant="outlined" color="primary" onClick={onViewChanged}>Leave Game</Button>
      </div>
    )
  }
}

GameStatus.propTypes = {
  onViewChanged: PropTypes.func,
}
