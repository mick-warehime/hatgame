import React, { Component, } from 'react';
import PropTypes from 'prop-types';

export default class LobbyView extends Component {

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

LobbyView.propTypes = {
  onViewChanged: PropTypes.func,
}