import React, { Component, } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import { Views } from '../../utils/constants';
import { FormControl } from '@material-ui/core';
import { Input } from '@material-ui/core';
import { InputLabel } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

export default class PhraseView extends Component {
  constructor(props) {
    super(props);
    this.state = {ready: false, phrases: ['','','']}
    this.setPhrase = this.setPhrase.bind(this)
    this.onSubmit = this.onSubmit.bind(this)
    //
  }

  componentDidMount () {
  //
  }

  onSubmit() {
  //
    console.log("submitted phrases")
    const {ready, phrases} = this.state
    this.setState({ready: !ready, phrases:phrases})
    const {socket} = this.props;
    socket.emit('submit_phrases', {phrases:phrases})
  }

  setPhrase(index, event){
    var {phrases, ready} = this.state
    phrases[index] = event.target.value
    this.setState({ready: ready, phrases: phrases})
    console.log(this.state)
  }

  render() {
    const {changeGameViewTo} = this.props;
    const {ready} = this.state;
    const buttonText = !ready ? "Ready!" : "Not Ready"
    const buttonColor = !ready ? "primary" : "secondary"
    return (
      <div>
        <Grid
          container
          spacing={1}
          direction="column"
          alignItems="center"
          justify="center"
          style={{ minHeight: '50vh' }}
        >
          <Grid item xs={6}>
            <Typography style={{ fontSize: 25 }}>Add 3 phrases to the
              <FontAwesomeIcon icon={['fas', 'hat-wizard']} />
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography style={{ fontSize: 15 }}>(nouns work best)</Typography>
          </Grid>
          <Grid item xs={9}>
            <FormControl>
              <InputLabel htmlFor="phrase1-input">phrase</InputLabel>
              <Input id="phrase1-input" disabled={ready} onChange={e => this.setPhrase(0, e)}/>
            </FormControl>
          </Grid>
          <Grid item xs={9}>
            <FormControl>
              <InputLabel htmlFor="phrase2-input">phrase</InputLabel>
              <Input id="phrase2-input" disabled={ready} onChange={e => this.setPhrase(1, e)} />
            </FormControl>
          </Grid>
          <Grid item xs={9}>
            <FormControl>
              <InputLabel htmlFor="phrase3-input">phrase</InputLabel>
              <Input id="phrase3-input" disabled={ready} onChange={e => this.setPhrase(2, e)}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <Button variant="contained" color={buttonColor} onClick={this.onSubmit}>
              {buttonText}
            </Button>

          </Grid>
        </Grid>
        <Button variant="contained" color={buttonColor} onClick={() => changeGameViewTo(Views.SUMMARY)}>
              Summary
        </Button>
      </div>
    )
  }
}

PhraseView.propTypes = {
  socket: PropTypes.any,
  changeGameViewTo: PropTypes.func,
}