import { useEffect, useState } from "react";
import { AppState, Text } from "react-native";
import EventSource, { EventSourceListener } from "react-native-sse";

type AlertEvent = "alert" | "relieve-alert";
const es = new EventSource<AlertEvent>("http://10.0.0.119:5000/alert-stream");
export default function AlertBox() {
	const [alertText, setAlertText] = useState("no alert");
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
			console.log("no alert");
			setAlertText("no Alert");
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
		<>
			<Text>{alertText}</Text>
		</>
	);
}
