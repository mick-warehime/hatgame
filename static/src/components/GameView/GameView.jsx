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
    const {changeViewTo, socket} = this.props
    return (
      <div className="game">
        <div className="left-panel">
          <GameStatus changeViewTo={changeViewTo} socket={socket}/>
        </div>
        <div className="right-panel">
          <GameBoard socket={socket}/>
        </div>
      </div>
    )
  }
}

GameView.propTypes = {
  changeViewTo: PropTypes.func,
  socket: PropTypes.any,
}