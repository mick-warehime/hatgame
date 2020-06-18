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
    this.onSubmit = this.onSubmit.bind(this)
    //
  }

  componentDidMount () {
  //
  }

  onSubmit() {
  //
    console.log("submitted phrases")
  }

  render() {
    const {boardViewChanged} = this.props;
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
              <Input id="phrase1-input" onChange={this.updateName}/>
            </FormControl>
          </Grid>
          <Grid item xs={9}>
            <FormControl>
              <InputLabel htmlFor="phrase2-input">phrase</InputLabel>
              <Input id="phrase2-input" onChange={this.updateRoom}/>
            </FormControl>
          </Grid>
          <Grid item xs={9}>
            <FormControl>
              <InputLabel htmlFor="phrase3-input">phrase</InputLabel>
              <Input id="phrase3-input" onChange={this.updateRoom}/>
            </FormControl>
          </Grid>
          <Grid item xs={3}>
            <Button variant="contained" color="primary" onClick={this.onSubmit}>
              <FontAwesomeIcon icon={['fas' , 'paper-plane']} size="2x"/>
            </Button>
          </Grid>
        </Grid>
        <Button variant="outlined" color="secondary" onClick={() => boardViewChanged(Views.SUMMARY)}>SUMMARY</Button>
      </div>
    )
  }
}

PhraseView.propTypes = {
  socket: PropTypes.any,
  boardViewChanged: PropTypes.func,
}