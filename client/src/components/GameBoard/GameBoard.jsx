import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Views } from '../../utils/constants';
import AudienceView from '../AudienceView/AudienceView';
import ActivePlayerView from '../ActivePlayerView/ActivePlayerView';
import PhraseView from '../PhraseView/PhraseView';
import TestView from '../TestView/TestView';

export default class GameBoard extends Component {
  constructor(props) {
    super(props);
    this.state = {view: Views.PHRASE}
    this.boardViewChanged = this.boardViewChanged.bind(this)
  }

  boardViewChanged(newView) {
    this.setState({view: newView})
  }

  render() {
    const {socket} = this.props;
    const {view} = this.state;
    switch (view) {
    case Views.ACTIVE_PLAYER:
      return <ActivePlayerView boardViewChanged={this.boardViewChanged} socket={socket}/>;
    case Views.AUDIENCE:
      return  <AudienceView boardViewChanged={this.boardViewChanged} socket={socket}/>;
    case Views.PHRASE:
      return  <PhraseView boardViewChanged={this.boardViewChanged} socket={socket}/>;
    case Views.TEST:
      return  <TestView boardViewChanged={this.boardViewChanged} socket={socket}/>;
    default:
      return (
        <div>
          <h1>Sorry not implemented</h1>
        </div>
      )
    }
  }
}

GameBoard.propTypes = {
  onViewChanged: PropTypes.func,
  socket: PropTypes.any,
}
