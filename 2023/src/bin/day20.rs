use std::collections::{HashMap, VecDeque};

use aoc2023_rust::*;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
enum Pulse {
    Low,
    High,
}

#[derive(Debug)]
struct Message {
    src: String,
    pulse: Pulse,
    dst: String,
}

trait Module: std::fmt::Debug {
    fn name(&self) -> &str;
    fn process(&mut self, msg: &Message) -> Vec<Message>;
    fn conjunction_state(&mut self) -> &HashMap<String, Pulse> {
        panic!("Only implemented for Conjunction!");
    }
}

#[derive(Debug)]
struct FlipFlop {
    name: String,
    outputs: Vec<String>,
    on: bool,
}

impl FlipFlop {
    fn new(name: String, outputs: Vec<String>) -> FlipFlop {
        FlipFlop {
            name,
            outputs,
            on: false,
        }
    }
}

impl Module for FlipFlop {
    fn name(&self) -> &str {
        &self.name
    }

    fn process(&mut self, msg: &Message) -> Vec<Message> {
        let out_pulse = match msg.pulse {
            Pulse::High => None,
            Pulse::Low => {
                self.on = !self.on;
                if self.on {
                    Some(Pulse::High)
                } else {
                    Some(Pulse::Low)
                }
            }
        };
        match out_pulse {
            Some(pulse) => self
                .outputs
                .iter()
                .map(|dst| Message {
                    src: self.name.clone(),
                    dst: dst.clone(),
                    pulse,
                })
                .collect(),
            None => vec![],
        }
    }
}

#[derive(Debug)]
struct Conjunction {
    name: String,
    inputs: Vec<String>,
    outputs: Vec<String>,
    input_history: HashMap<String, Pulse>,
}

impl Conjunction {
    fn new(name: String, inputs: Vec<String>, outputs: Vec<String>) -> Conjunction {
        // Default input_history to low for each input.
        let input_history = inputs
            .iter()
            .map(|input| (input.clone(), Pulse::Low))
            .collect();
        Conjunction {
            name,
            inputs,
            outputs,
            input_history,
        }
    }
}

impl Module for Conjunction {
    fn name(&self) -> &str {
        &self.name
    }

    fn process(&mut self, msg: &Message) -> Vec<Message> {
        // Update input history.
        self.input_history.insert(msg.src.clone(), msg.pulse);

        // If all inputs are high, then low, else high.
        let pulse = if self
            .inputs
            .iter()
            .all(|input| self.input_history[input] == Pulse::High)
        {
            Pulse::Low
        } else {
            Pulse::High
        };
        self.outputs
            .iter()
            .map(|dst| Message {
                src: self.name.clone(),
                dst: dst.clone(),
                pulse,
            })
            .collect()
    }

    fn conjunction_state(&mut self) -> &HashMap<String, Pulse> {
        &self.input_history
    }
}

#[derive(Debug)]
struct Broadcast {
    outputs: Vec<String>,
}

impl Module for Broadcast {
    fn name(&self) -> &str {
        "broadcaster"
    }

    fn process(&mut self, msg: &Message) -> Vec<Message> {
        self.outputs
            .iter()
            .map(|dst| Message {
                src: self.name().into(),
                dst: dst.clone(),
                pulse: msg.pulse,
            })
            .collect()
    }
}

fn button() -> Message {
    Message {
        src: "button".into(),
        dst: "broadcaster".into(),
        pulse: Pulse::Low,
    }
}

fn part1(input: &str) {
    let modules = load_modules(input);
    let mut name_to_module: HashMap<String, Box<dyn Module>> = HashMap::new();
    for module in modules {
        name_to_module.insert(module.name().into(), module);
    }

    let mut num_low_pulses = 0;
    let mut num_high_pulses = 0;
    for _cycle in 0..1000 {
        // println!("Processing iteration {}", cycle);
        let mut queue = VecDeque::new();
        queue.push_back(button());
        while let Some(msg) = queue.pop_front() {
            // println!("Processing {:?}", msg);
            if msg.pulse == Pulse::Low {
                num_low_pulses += 1;
            } else {
                num_high_pulses += 1;
            }
            let Some(module) = name_to_module.get_mut(&msg.dst) else {
                // println!("Unknown dst for message {:?}", msg);
                continue;
            };
            let new_msgs = module.process(&msg);
            for new_msg in new_msgs {
                queue.push_back(new_msg);
            }
        }
    }
    println!(
        "low * high: {} * {} = {}",
        num_low_pulses,
        num_high_pulses,
        num_low_pulses * num_high_pulses
    );
}

// bb goes to rx
// bb is a conjunction of xc, ct, kp, ks, so we want all 4 to be high.
fn part2(input: &str) {
    let modules = load_modules(input);
    let mut name_to_module: HashMap<String, Box<dyn Module>> = HashMap::new();
    for module in modules {
        name_to_module.insert(module.name().into(), module);
    }

    // Loop checkers.
    let mut first_high_bb_input = HashMap::new();
    let mut second_high_bb_input = HashMap::new();
    let mut num_buttons: i64 = 0;
    loop {
        let mut queue = VecDeque::new();
        queue.push_back(button());
        num_buttons += 1;
        while let Some(msg) = queue.pop_front() {
            if msg.dst == "rx" && msg.pulse == Pulse::Low {
                println!("Found low pulse on rx after {} buttons", num_buttons);
                break;
            }
            let Some(module) = name_to_module.get_mut(&msg.dst) else {
                continue;
            };
            let new_msgs = module.process(&msg);
            if module.name() == "bb" {
                let state = module.conjunction_state();
                for (input, pulse) in state {
                    if *pulse == Pulse::High {
                        let first_high = first_high_bb_input.get(input);
                        let second_high = second_high_bb_input.get(input);
                        if first_high.is_none() {
                            first_high_bb_input.insert(input.clone(), num_buttons);
                        } else if second_high.is_none() {
                            if num_buttons != *first_high.unwrap() {
                                second_high_bb_input.insert(input.clone(), num_buttons);
                            }
                        }
                    }
                }
                // Just gonna assume product is the LCM.
                let mut product = 1;
                if second_high_bb_input.len() == state.len() {
                    for (input, &first_high) in &first_high_bb_input {
                        let second_high = second_high_bb_input[input];
                        assert_eq!(first_high, second_high - first_high);
                        product *= first_high;
                    }
                    println!("Product of cycles is {}", product);
                    return;
                }
            }
            for new_msg in new_msgs {
                queue.push_back(new_msg);
            }
        }
    }
}

fn load_modules(input: &str) -> Vec<Box<dyn Module>> {
    // Traverse twice so we can hook up inputs on the 2nd pass.
    let mut name_to_type_and_outputs: HashMap<String, (char, Vec<String>)> = HashMap::new();
    for line in input.lines() {
        let (name, outputs) = line.split_once(" -> ").unwrap();
        let type_c = name.chars().nth(0).unwrap();
        let name = if type_c == 'b' {
            name.to_string()
        } else {
            name[1..].to_string()
        };
        let outputs: Vec<String> = outputs.split(", ").map(|s| s.to_string()).collect();
        name_to_type_and_outputs.insert(name, (type_c, outputs));
    }
    let mut name_to_inputs: HashMap<String, Vec<String>> = HashMap::new();
    for (name, (_type_c, outputs)) in &name_to_type_and_outputs {
        for output in outputs {
            name_to_inputs
                .entry(output.clone())
                .or_insert_with(Vec::new)
                .push(name.clone());
        }
    }

    let mut modules: Vec<Box<dyn Module>> = Vec::with_capacity(name_to_type_and_outputs.len());
    for (name, (type_c, outputs)) in name_to_type_and_outputs {
        let module: Box<dyn Module> = match type_c {
            '%' => Box::new(FlipFlop::new(name, outputs)),
            '&' => {
                let inputs = name_to_inputs.get(&name).unwrap();
                Box::new(Conjunction::new(name, inputs.clone(), outputs))
            }
            'b' => Box::new(Broadcast { outputs }),
            _ => panic!("Unknown module type: {}", type_c),
        };
        modules.push(module);
    }

    modules
}
