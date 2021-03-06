import React, { useContext } from "react";
import Button from "@material-ui/core/Button";
import axios from "axios";
import TextField from "@material-ui/core/TextField";
import { Grid } from "@material-ui/core";
import YobaContext from "../context/YobaContext";
import cookie from 'react-cookies';

const InputUrl = (props) => {
  const { actions, states } = useContext(YobaContext);

  // const temp = localStorage.getItem("loginStorage");
  const temp = cookie.load('data');

  const checkUrl = () => {
    try {
      axios
        .get("http://localhost:8000/api/analysis_url", {
          headers: { "Content-Type": "multipart/form-data" },
          params: {
            url: states.url,
          },
        })
        .then((response) => {
          const data = response.data;
          // console.log(data);
          if (data.result === false) {
            alert("wrong url. please, check url.");
          } else {
            actions.setPlatform(data.result[0]);
            actions.setVideoid(data.result[1]);
            props.toggleInput(true);
          }
        })
        .catch(function (error) {
          if (error.response.status === 400) {
            alert("wrong url. please, check url.");
          }
          // console.log(error);
        });
    } catch (e) {
      console.log(e);
    }
  };

  const onClick = () => {
    try {
      axios
        .get("http://localhost:8000/api/login", {
          headers: { "Content-Type": "multipart/form-data" },
          params: {
            email: temp.email,
            uuid: temp.uuid
          },
        })
        .then((response) => {
          const data = response.data;
          // console.log(data);

          // localStorage.setItem("loginStorage", JSON.stringify(data));
          cookie.save('data',JSON.stringify(data),{path:'/'})
          // props.toggleInput(true);
          // props.setUrl(url);
          if (props.input === true) {
            actions.setPlatform();
            actions.setVideoid();
            actions.setUrl();
            props.toggleInput(false);
            alert("reset");
          } else {
            checkUrl();
          }
        })
        .catch(function (error) {
          if (error.response.status === 401) {
            // localStorage.removeItem("loginStorage");
            cookie.remove('data');
            props.toggleLogin(false);
            props.toggleInput(false);
            alert("please, you need sign in again.");
          }
        });
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Grid>
      <Grid
        container
        alignItems="center"
        direction="row"
        justify="center"
        style={{ paddingTop: 40, paddingBottom: 10 }}
      >
        <Grid xs={2} style={{ marginRight: 20 }}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            name="url"
            label="url"
            type="url"
            id="url"
            fullWidth
            onChange={(e) => {
              actions.setUrl(e.target.value);
            }}
          />
        </Grid>

        <Grid>
          <Button variant="contained" color="secondary" onClick={onClick}>
            Input URL
          </Button>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default InputUrl;
