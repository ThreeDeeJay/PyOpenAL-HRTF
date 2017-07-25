# PyOpenAL

PyOpenAL provides OpenAL bindings for python as well as an interface to them.

It even provides a simple way to open OGG Vorbis and OGG Opus files, if used together with [PyOgg](https://github.com/Zuzu-Typ/PyOgg).

PyOpenAL requires a dynamic OpenAL library (OpenAL32.dll). 
You can use the [official OpenAL library](http://www.openal.org/) (deprecated) or the much better sounding [OpenAL Soft library](http://kcat.strangesoft.net/openal.html), which is still actively developed (or any other OpenAL compatible library).

PyOpenAL provides OpenAL bindings, as you would find them in C++, meaning you can follow any [OpenAL C++ tutorial](http://www.openal.org/documentation/) with Python.
OpenAL's methods expect C types as arguments, which means you will have to convert Python's types to C types using [ctypes](https://docs.python.org/3/library/ctypes.html) if you want to use them directly.
Don't worry though, PyOpenAL can be used without the need to do that.

I removed the support for ALUT, because it is basically impossible to build nowadays. If you want ALUT support, please use the original [PyOpenAL from forrestv](https://github.com/forrestv/PyOpenAL)

### Examples (with PyOgg)
##### Playing a file

	from openal import * 
	
	# even though we use PyOgg, we don't have to import it ourselves, 
	# PyOpenAL does that for us (if it can find it)
	
	import time

	# open "test.opus"
	source = oalLoadFile("test.opus")

	source.play()

	while source.get_state() == AL_PLAYING:
		# wait until the file is done playing
		time.sleep(1)
		
	# release resources (don't forget this)
	oalQuit()
		
##### Streaming a file

	from openal import *

	# it is not required to do this, it's just to show off it exists
	pyoggSetStreamBufferSize(4096*4)
	oalSetStreamBufferCount(4)

	sourceStream = oalStreamFile("test.ogg")

	sourceStream.play()

	while sourceStream.get_state() == AL_PLAYING:
		# do stuff
		sourceStream.update()
		
	oalQuit()
	
### Using OpenAL functions

	# here we only import OpenAL's functions 
	# (in case you don't need / want PyOpenAL's functions / classes)
	from openal._al import *
	from openal._alc import *

	[...]
	
	# it's as simple as that:
	alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED)
	
	# or a little more complicated, it really depends:
	alSourceUnqueueBuffers(source_id, 1, ctypes.pointer(ctypes.c_uint(buffer_ids[id])))
	
	[...]

### Reference (for PyOpenAL's own classes and functions)

	<method> oalInit(device_specifier = None, context_attr_list = None) -> None
		# initializes PyOpenAL
		# this is called automatically, unless you set OAL_DONT_AUTO_INIT
			<c_char_p> device_specifier # you can set a custom device with this
			<c_int_p> context_attr_list # you can pass additional arguments to context creation
		
	<method> oalGetInit() -> <bool> initialized
		# finds out wether or not PyOpenAL is initialized
		
	<method> oalGetContext() -> <int> context
		# returns the context used by PyOpenAL
		
	<method> oalGetDevice() -> <int> device
		# returns the device used by PyOpenAL
		
	<method> oalSetAutoInit(val) -> None
		# changes wether or not PyOpenAL initializes automatically
			<bool> val # wether or not to auto-init
			
	<method> oalQuit() -> None
		# exits out of OpenAL and destroys all existing Sources and Buffers
		
	<method> oalLoadFile(path, ext_hint = None) -> Source
		# loads an Ogg Vorbis / Opus file to a Source object
			<str> path # path to the file (relative or absolute)
			<str> ext_hint # if the filetype is not ogg, vorbis or opus, you should supply a hint to the extension
			
	<method> oalStreamFile(path, ext_hint = None) -> SourceStream
		# loads an Ogg Vorbis / Opus file to a SourceStream object, that streams the data
		# you should use this instead of Source for Soundtracks or other long tracks (as it uses less memory)
		# you will have to update it frequently to avoid suffocation of the stream
		# you can neither rewind nor loop a SourceStream (currently)
			<str> path # path to the file (relative or absolute)
			<str> ext_hint # if the filetype is not ogg, vorbis or opus, you should supply a hint to the extension

	<class> openal.Listener()
		# class for hadling the listener (you)
		# an instance of this class is created when you import PyOpenAL.
		# it can be retrieved using oalGetListener()
		# you do NOT have to create an instance yourself
		
		<method> Listener.move(v)
			# move the listener by v
				<tuple or list> v # a translation vector represented as (x, y, z)
		
		<method> Listener.move_to(v)
			# set the listener's position to v
				<tuple or list> v # a position vector represented as (x, y, z)
				
		<method> Listener.set_position(v)
			# see Listener.move_to
			
		<method> Listener.set_orientation(v)
			# sets the listener's orientation to v
				<tuple or list> v # orientation represented as (frontX, frontY, frontZ, upX, upY, upZ)
				
		<method> Listener.set_velocity(v)
			# sets the listener's velocity to v
				<tuple or list> v # velocity represented as (vX, vY, vZ)
				
		<method> Listener.set_gain(value)
			# sets the listener's gain (volume) to value
				<float> value
				
	<method> openal.oalGetListener() -> Listener
		# returns PyOpenAL's Listener
		
	<class> openal.Buffer(*args)
		# class for managing OpenAL buffers
			<PYOGG-File or tuple or list> args # what to fill the buffer with (either y PyOgg file or a tuple / list with [format, data, length, frequency])
		
		<method> Buffer.fill(*args) -> None
			# fill the buffer
				<PYOGG-File or tuple or list> args # what to fill the buffer with (either y PyOgg file or a tuple / list with [format, data, length, frequency])
			
		<method> Buffer.destroy() -> None
			# destroy this buffer
			
	<class> openal.StreamBuffer(stream, count)
		# class for managing OpenAL buffers for audio streaming
			<PYOGG-Stream> stream # from where to get the data
			<int> count # how many buffers to create (usually OAL_STREAM_BUFFER_COUNT, which is 2 initially)
		
		<method> Buffer.fill_buffer(id_) -> None
			# fill the buffer
				<int> id_ # load some data into this buffer
			
		<method> Buffer.destroy() -> None
			# destroy this streambuffer
			
	<class> openal.Source(buffer_ = None)
		# class for managing a source
			<Buffer> buffer_ # where this source finds it's data
			
		<method> Source.play() -> None
			# starts playing
			
		<method> Source.stop() -> None
			# stops playback
			
		<method> Source.pause() -> None
			# pauses playback (use play to resume)
			
		<method> Source.rewind() -> None
			# goes back to the start of the track
			
		<float> Source.pitch
			# the source's current pitch
			
		<float> Source.gain
			# the source's current gain
			
		<float> Source.max_distance
			# the source's current max_distance
			
		<float> Source.rolloff_factor
			# the source's current rolloff_factor
			
		<float> Source.reference_distance
			# the source's current reference_distance
			
		<float> Source.min_gain
			# the source's current min_gain
			
		<float> Source.max_gain
			# the source's current max_gain
			
		<float> Source.cone_outer_angle
			# the source's current cone_outer_angle
			
		<float> Source.cone_inner_angle
			# the source's current cone_inner_angle
			
		<float> Source.cone_outer_gain
			# the source's current cone_outer_gain
			
		<vec3> Source.position
			# the source's current position (use .x, .y, and .z to access it's items or .toTuple())
			
		<vec3> Source.velocity
			# the source's current velocity (use .x, .y, and .z to access it's items or .toTuple())
			
		<vec3> Source.direction
			# the source's current velocity (use .x, .y, and .z to access it's items or .toTuple())
			
		<bool> Source.relative
			# wether or not the source is relative to the listener
			
		<int> Source.source_type
			# the source's current source_type (either AL_UNDETERMINED, AL_STATIC or AL_STREAMING)
			
		<method> Source.set_pitch(value) -> None
			# set the pitch for this source
				<float> value # pitch
				
		<method> Source.set_gain(value) -> None
			# set the gain for this source
				<float> value # gain
				
		<method> Source.set_max_distance(value) -> None
			# set the max_distance for this source
				<float> value # max_distance
				
		<method> Source.set_rolloff_factor(value) -> None
			# set the rolloff_factor for this source
				<float> value # rolloff_factor
				
		<method> Source.set_reference_distance(value) -> None
			# set the reference_distance for this source
				<float> value # reference_distance
				
		<method> Source.set_min_gain(value) -> None
			# set the min_gain for this source
				<float> value # min_gain
				
		<method> Source.set_max_gain(value) -> None
			# set the max_gain for this source
				<float> value # max_gain
				
		<method> Source.set_cone_outer_gain(value) -> None
			# set the cone_outer_gain for this source
				<float> value # cone_outer_gain
				
		<method> Source.set_cone_inner_angle(value) -> None
			# set the cone_inner_angle for this source
				<float> value # cone_inner_angle
				
		<method> Source.set_cone_outer_angle(value) -> None
			# set the cone_outer_angle for this source
				<float> value # cone_outer_angle
				
		<method> Source.set_position(value) -> None
			# set the position for this source
				<tuple or list> value # position
				
		<method> Source.set_velocity(value) -> None
			# set the velocity for this source
				<tuple or list> value # velocity
				
		<method> Source.set_looping(value) -> None
			# set the looping for this source
				<bool> value # looping
				
		<method> Source.set_direction(value) -> None
			# set the direction for this source
				<tuple or list> value # direction
				
		<method> Source.set_source_relative(value) -> None
			# set the source_relative for this source
				<bool> value # source_relative
				
		<method> Source.set_source_type(value) -> None
			# set the source_type for this source
				<int> value # source_type
				
		<method> Source.set_buffer(buffer_) -> None
			# set the buffer for this source
				<Buffer> value # buffer
				
		<method> Source.get_state() -> <int> state of the Source (e.g. AL_PLAYING, AL_STOPPED,etc.)
			# get the current state of the source
			
	<class> openal.SourceStream(stream)
		# class for managing a source in streaming mode
			<PYOGG-Stream> stream # where the buffer gets it's data from
			
		<method> update() -> <bool> playing
			# load more data to play (if necessary). 
			# if you don't call this frequently, the source will stop playing after it reaches the last buffer
			# in that case you should consider increasing the buffer size or amount using oalSetStreamBufferCount or pyoggSetStreamBufferSize
			
		# The other methods and variables are the same as in Source 
		# (note that you can't loop, because the file can be read only once (by now))