import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Views } from '../../utils/constants';
import AudienceView from '../AudienceView/AudienceView';
import ActivePlayerView from '../ActivePlayerView/ActivePlayerView';
import PhraseView from '../PhraseView/PhraseView';
import SummaryView from '../SummaryView/SummaryView';
import TestView from '../TestView/TestView';

export default class GameBoard extends Component {
  constructor(props) {
    super(props);
    this.state = {view: Views.PHRASE}
    this.changeGameViewTo = this.changeGameViewTo.bind(this)
  }

  changeGameViewTo(newView) {
    this.setState({view: newView})
  }

  render() {
    const {socket} = this.props;
    const {view} = this.state;
    switch (view) {
    case Views.ACTIVE_PLAYER:
      return <ActivePlayerView changeGameViewTo={this.changeGameViewTo} socket={socket}/>;
    case Views.AUDIENCE:
      return  <AudienceView changeGameViewTo={this.changeGameViewTo} socket={socket}/>;
    case Views.PHRASE:
      return  <PhraseView changeGameViewTo={this.changeGameViewTo} socket={socket}/>;
    case Views.SUMMARY:
      return  <SummaryView changeGameViewTo={this.changeGameViewTo} socket={socket}/>;
    case Views.TEST:
      return  <TestView changeGameViewTo={this.changeGameViewTo} socket={socket}/>;
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
  socket: PropTypes.any,
}
