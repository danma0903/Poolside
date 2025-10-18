import { useEffect, useState } from "react";
import { AppState, Text } from "react-native";
import EventSource, { EventSourceListener } from "react-native-sse";

type AlertEvent = "alert" | "relieve-alert";
const es = new EventSource<AlertEvent>("myurlplaceholder");
export default function AlertBox() {
	const [alertText, setAlertText] = useState("no alert");
	useEffect(() => {
		const alertHandler: EventSourceListener<AlertEvent, "alert"> = (event) => {
			console.log("alert_received");
			setAlertText("Alert");
		};
		const relieveAlertHandler: EventSourceListener<
			AlertEvent,
			"relieve-alert"
		> = (event) => {
			console.log("no alert");
			setAlertText("no Alert");
		};
		const appStateEventSub = AppState.addEventListener("change", (newState) => {
			if (newState === "active") {
				es.open();
				es.addEventListener("alert", alertHandler);
				es.addEventListener("relieve-alert", relieveAlertHandler);
			} else if (newState === "background" || newState === "inactive") {
				es.removeAllEventListeners();
				es.close();
			}
		});
		return () => {
			appStateEventSub.remove();
		};
	});
	return (
		<>
			<Text>{alertText}</Text>
		</>
	);
}
