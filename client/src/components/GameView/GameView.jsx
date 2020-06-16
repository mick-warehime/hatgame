import React, { Component} from 'react';
import PropTypes from 'prop-types';
import GameBoard from '../GameBoard/GameBoard';
import GameStatus from '../GameStatus/GameStatus';
import './GameView.css';

export default class GameView extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const {onViewChanged, socket} = this.props
    return (
      <div className="game">
        <div className="left-panel">
          <GameStatus onViewChanged={onViewChanged}/>
        </div>
        <div className="right-panel">
          <GameBoard  socket={socket}/>
        </div>
      </div>
    )
  }
}

GameView.propTypes = {
  onViewChanged: PropTypes.func,
  socket: PropTypes.any,
}