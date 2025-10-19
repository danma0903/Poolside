import { useEffect, useState } from "react";
import { AppState, Text, View, StyleSheet } from "react-native";
import EventSource, { EventSourceListener } from "react-native-sse";

type AlertEvent = "alert" | "relieve-alert";
const es = new EventSource<AlertEvent>("http://10.0.0.119:5000/alert-stream");
export default function AlertBox() {
	const [alertText, setAlertText] = useState("No Detection");
	useEffect(() => {
		const alertHandler: EventSourceListener<AlertEvent, "alert"> = (event) => {
			console.log("alert_received");
			console.log(event.data);
			setAlertText("Alert");
			console.log(alertText);
		};
		const relieveAlertHandler: EventSourceListener<
			AlertEvent,
			"relieve-alert"
		> = (event) => {
			setAlertText("No Detection");
		};
		es.open();
		console.log("handlers added");
		es.addEventListener("alert", alertHandler);
		es.addEventListener("relieve-alert", relieveAlertHandler);
		// const appStateEventSub = AppState.addEventListener("change", (newState) => {
		// 	if (newState === "active") {
		// 		es.open();
		// 		console.log("handlers added");
		// 		es.addEventListener("alert", alertHandler);
		// 		es.addEventListener("relieve-alert", relieveAlertHandler);
		// 	} else if (newState === "background" || newState === "inactive") {
		// 		es.removeAllEventListeners();
		// 		es.close();
		// 	}
		// });
		return () => {
			es.removeAllEventListeners();
			es.close();
			// appStateEventSub.remove();
		};
	}, []);
	return (
		(alertText === "Alert") ?
		<View style={styles.alertOverlay}>
			<Text>{alertText}</Text>
		</View> :
		<></>
	);
}

const styles = StyleSheet.create({
	alertOverlay: {
		position: "absolute",
		top: 5,
		left: 5,
		backgroundColor: "rgba(255,0,0,0.7)",
		paddingHorizontal: 8,
		paddingVertical: 4,
		borderRadius: 4,
	},
});
