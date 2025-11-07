# EmotiKeys – Project & Development Plan (Condensed Version)

## 1. Introduction

EmotiKeys is an interactive web experience that transforms emotions into sound. At the center of the webpage, users can interact with a hand-drawn 2D character to choose an emotion, then express it by drawing across a 20×10 grid with their mouse. Each emotion generates different colors and piano tones, creating a “musical emotion canvas.” The character’s facial expressions and subtle movements change according to the selected mood, adding a playful and immersive touch.
This project runs for 3 weeks (06 Nov 2025 – 28 Nov 2025), progressing from a basic prototype to a fully functional version.

## 2. Product Goal

To provide a simple and intuitive way for users to visually and musically express their emotions on a webpage, turning emotional input into dynamic sound and visual output that forms a personal emotion-based music artwork.

### 3.Product Backlog (Condensed – 13 Items)


| **ID** | **Item**                | **Description**                                        | **Priority** |
| -------- | ------------------------- | -------------------------------------------------------- | -------------- |
| PB01   | Basic project setup     | Set up webpage and Python backend structure            | P1           |
| PB02   | Main UI & character     | Layout with character + 5 emotion options + grid       | P1           |
| PB03   | 20×10 grid interaction | Detect mouse position on the grid                      | P1           |
| PB04   | Emotion selection       | User can choose one of 5 emotions                      | P1           |
| PB05   | Emotion color styling   | Colors and visual style vary per emotion               | P1           |
| PB06   | Drawing effects         | Mouse movement “paints” emotional colors on grid     | P2           |
| PB07   | Character expressions   | Character face changes with emotion                    | P2           |
| PB08   | Character micro-motion  | Character slightly shifts position near emotion labels | P2           |
| PB09   | Sound integration       | Trigger piano notes through interaction                | P1           |
| PB10   | Emotion–music rules    | Different tempo, rhythm, note length per emotion       | P1           |
| PB11   | Position→pitch mapping | Grid position influences pitch or volume               | P2           |
| PB12   | Clear & reset           | User can clear and restart drawing                     | P3           |
| PB13   | Export function         | Export the artwork or save the data                    | P3           |

## 4. 3-Week Development Plan (Sprint Overview)


| **Sprint** | **Dates**    | **Sprint Goal**                                                                              |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------- |
| Sprint 1   | 11/06–11/12 | Build the basic structure and main UI, enabling emotion selection and basic grid interaction |
| Sprint 2   | 11/13–11/19 | Implement core emotion-based visuals and sounds to create expressive experience              |
| Sprint 3   | 11/20–11/28 | Enhance interaction details and add export features to finalize the project                  |

## 5. Sprint 1 Plan & Deliverable

### Sprint 1 Goal

Build the basic structure and main interface, enabling emotion selection and initial grid interaction.


### Scope of Work

* PB01 Basic project setup
* PB02 Main UI & character
* PB03 Grid interaction
* PB04 Emotion selection


### Deliverable (Increment v0.1)

A basic prototype where users can see the interface, choose an emotion, and interact with the grid.


## 6. Sprint 2 Plan & Deliverable

### Sprint 2 Goal

Develop core emotional expression through visual and sound feedback.

### Scope of Work

* PB05 Emotion color styling
* PB06 Drawing effects
* PB07 Character expressions
* PB09 Sound integration
* PB10 Emotion–music rules

### Deliverable (Increment v0.5)

A more expressive version where users can draw emotions and hear distinct piano responses reflecting each mood.


## 7. Sprint 3 Plan & Deliverable

### Sprint 3 Goal

Refine details, enhance interaction, and support exporting user creations.

### Scope of Work

* PB08 Character micro-motion
* PB11 Position → pitch mapping
* PB12 Clear & reset
* PB13 Export function

### Deliverable (Release v1.0)

A complete, polished version with smooth interaction, visual-sound expression, and export options.
