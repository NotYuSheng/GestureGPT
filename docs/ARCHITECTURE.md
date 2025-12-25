# GestureGPT Architecture

## System Overview

GestureGPT is a sign language API that **retrieves pre-recorded ASL videos** from a dataset rather than generating them.

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Request                              │
│                   "Hello, how are you?"                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Backend (GestureGPT)                        │
│                /v1/chat/completions                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      ┌──────────────┐      ┌─────────────────┐
      │  LLM Service │      │ Direct Endpoint │
      │ (Text Gen)   │      │                 │
      └──────┬───────┘      └─────────────────┘
             │
     ┌───────┴────────┐
     │  LLM Provider  │
     │ OpenAI/Claude/ │
     │   Local LLM    │
     └───────┬────────┘
             │
             ▼
    ┌────────────────┐
    │ Text Response  │
    │ "Hello! I feel │
    │ good. Thank    │
    │ you ask!"      │
    └────────┬───────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Sign Language Mapping Service                       │
│                                                                  │
│  1. Tokenize text: ["HELLO", "I", "FEEL", "GOOD", "THANK",     │
│                     "YOU", "ASK"]                               │
│  2. Map to sign glosses (ASL grammar)                           │
│  3. Look up video files for each sign                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ASL Video Dataset Repository                        │
│                                                                  │
│  Pre-recorded sign videos organized by:                         │
│  - Individual signs (WLASL, ASL-LEX, etc.)                     │
│  - Fingerspelling alphabet                                      │
│  - Common phrases                                               │
│                                                                  │
│  Example structure:                                             │
│  videos/                                                        │
│    ├── signs/                                                   │
│    │   ├── HELLO.mp4                                           │
│    │   ├── FEEL.mp4                                            │
│    │   ├── GOOD.mp4                                            │
│    │   └── THANK-YOU.mp4                                       │
│    ├── fingerspell/                                            │
│    │   ├── A.mp4                                               │
│    │   ├── B.mp4                                               │
│    │   └── ...                                                 │
│    └── phrases/                                                │
│        ├── HOW-ARE-YOU.mp4                                     │
│        └── ...                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                Video Stitching Service                           │
│                                                                  │
│  1. Retrieve individual sign videos                             │
│  2. Concatenate videos in sequence                              │
│  3. Add transitions (optional)                                  │
│  4. Generate final composite video                              │
│  5. Cache result for reuse                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Final MP4 Video │
              │  (Stitched ASL)  │
              └─────────┬────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Response                                  │
│  {                                                               │
│    "choices": [{                                                 │
│      "message": {                                                │
│        "content": "Hello! I feel good. Thank you ask!"          │
│      },                                                          │
│      "video_url": "/videos/cached_response_abc123.mp4"          │
│    }]                                                            │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Text Input Processing
- Receives user message via OpenAI-compatible API
- Routes to LLM for response generation

### 2. LLM Response Generation
- **Placeholder**: Canned ASL-friendly responses
- **OpenAI/Claude**: Real LLM with ASL-formatted prompts
- **Local LLM**: Ollama/LM Studio for privacy

### 3. Sign Language Mapping Service
**Key component that needs implementation:**

```python
class SignMapper:
    def text_to_signs(self, text: str) -> List[str]:
        """
        Convert English text to ASL glosses

        Input: "Hello! I feel good."
        Output: ["HELLO", "I", "FEEL", "GOOD"]
        """
        # Tokenize and map to ASL glosses
        # Remove articles, adjust grammar for ASL
        pass

    def get_video_paths(self, signs: List[str]) -> List[str]:
        """
        Map sign glosses to video file paths

        Input: ["HELLO", "FEEL", "GOOD"]
        Output: [
            "videos/signs/HELLO.mp4",
            "videos/signs/FEEL.mp4",
            "videos/signs/GOOD.mp4"
        ]
        """
        # Look up videos in dataset
        # Fall back to fingerspelling if sign not found
        pass
```

### 4. ASL Video Dataset
**Recommended datasets:**

1. **WLASL (Word-Level ASL)**
   - 2,000+ ASL signs
   - Multiple signers
   - URL: https://dxli94.github.io/WLASL/

2. **ASL-LEX**
   - 2,700+ lexical signs
   - Phonological features
   - URL: https://asllex.org/

3. **SignBank**
   - Comprehensive ASL dictionary
   - High-quality videos

4. **Spreadthesign**
   - International sign languages
   - Multiple countries

### 5. Video Stitching Service
```python
class VideoStitcher:
    def stitch_videos(self, video_paths: List[str]) -> str:
        """
        Concatenate individual sign videos

        Input: ["HELLO.mp4", "FEEL.mp4", "GOOD.mp4"]
        Output: "output/response_abc123.mp4"
        """
        # Use ffmpeg or opencv to concatenate
        # Add smooth transitions between signs
        # Return path to final video
        pass
```

## Video Retrieval Strategy

```
Text: "Hello, how are you?"
         ↓
ASL Mapping: ["HELLO", "HOW", "YOU"]
         ↓
Video Lookup:
         ├─ "HELLO" → videos/signs/HELLO.mp4 ✓
         ├─ "HOW" → videos/signs/HOW.mp4 ✓
         └─ "YOU" → videos/signs/YOU.mp4 ✓
         ↓
Stitch videos → Final output
```

### Fallback Strategy

```
Sign: "CRYPTOCURRENCY" (not in dataset)
         ↓
Check alternatives:
         ├─ Exact match? ✗
         ├─ Similar sign? ✗
         └─ Fingerspell? ✓
         ↓
Fingerspell: C-R-Y-P-T-O-C-U-R-R-E-N-C-Y
         ↓
Retrieve: [C.mp4, R.mp4, Y.mp4, P.mp4, ...]
```

## Caching Strategy

```
┌─────────────────────────────────────┐
│   Request: "Hello, how are you?"    │
└──────────────┬──────────────────────┘
               ▼
         Check cache?
               │
        ┌──────┴──────┐
        ▼             ▼
      Found         Not Found
        │             │
        ▼             ▼
  Return cached   Generate video
  video URL       Stitch signs
        │             │
        └──────┬──────┘
               ▼
         Return response
```

## Current vs Target Implementation

### Current (Placeholder)
```python
# app/services/sign_language_service.py
def generate_video(text):
    # Creates demo animation
    return "demo_video.mp4"
```

### Target (Dataset-based)
```python
# app/services/sign_language_service.py
def generate_video(text):
    # 1. Map text to ASL glosses
    signs = sign_mapper.text_to_signs(text)

    # 2. Retrieve video paths
    video_paths = dataset.get_videos(signs)

    # 3. Stitch videos
    final_video = stitcher.concatenate(video_paths)

    # 4. Cache result
    cache.store(text, final_video)

    return final_video
```

## Directory Structure (Proposed)

```
GestureGPT/
├── app/
│   ├── services/
│   │   ├── llm_service.py          # LLM text generation
│   │   ├── sign_mapper.py          # Text → ASL glosses
│   │   ├── video_retrieval.py      # Retrieve from dataset
│   │   └── video_stitcher.py       # Concatenate videos
│   └── ...
├── datasets/
│   ├── wlasl/                      # WLASL dataset
│   │   ├── signs/
│   │   │   ├── HELLO.mp4
│   │   │   ├── GOOD.mp4
│   │   │   └── ...
│   │   └── metadata.json
│   ├── fingerspell/
│   │   ├── A.mp4
│   │   ├── B.mp4
│   │   └── ...
│   └── phrases/
│       └── ...
└── cache/                          # Cached stitched videos
    └── ...
```

## Implementation Priority

1. **Phase 1**: Sign Mapping Service
   - Text tokenization
   - ASL gloss mapping
   - Basic grammar conversion

2. **Phase 2**: Dataset Integration
   - Download WLASL dataset
   - Build video index
   - Implement lookup service

3. **Phase 3**: Video Stitching
   - Concatenation logic
   - Smooth transitions
   - Performance optimization

4. **Phase 4**: Caching & Optimization
   - Cache common phrases
   - Optimize video delivery
   - Add CDN support

## Performance Considerations

- **Video caching**: Pre-stitch common phrases
- **Lazy loading**: Load datasets on demand
- **CDN delivery**: Serve videos from CDN
- **Compression**: Optimize video file sizes
- **Parallel processing**: Stitch videos concurrently

## Next Steps

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for step-by-step instructions on implementing the dataset-based approach.
