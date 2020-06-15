import React, { Component } from 'react';
import { Views } from '../../utils/constants';
import LobbyView from '../LobbyView/LobbyView';
import GameView from '../GameView/GameView';


export default class Controller extends Component {
    constructor(props) {
      super(props);
      this.state = {view: Views.LOBBY}
      this.onViewChanged = this.onViewChanged.bind(this)
    }

    onViewChanged() {
        const {view} = this.state
        var newView = Views.LOBBY
        if (view == Views.LOBBY){
            newView = Views.GAME
            }
        this.setState({view: newView})
    }

    render() {
       const { view } = this.state;
       switch (view) {
      case Views.LOBBY:
        return <LobbyView onViewChanged={this.onViewChanged}/>;
      case Views.GAME:
        return  <GameView onViewChanged={this.onViewChanged}/>;
      default:
       return (
       <div>
        <h1>Sorry not implemented</h1>
        </div>
       )
        }
    }
}
