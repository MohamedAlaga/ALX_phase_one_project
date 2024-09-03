import React from 'react'

const Getapp = () => {
  return (
    <div className="flex w-full flex-col gap-3 whitespace-nowrap xl:flex-row">
    <button 
      type="button"
      title="App Store"
      icon="/apple.svg"
      variant="btn_white"
      full
    />
    <button 
      type="button"
      title="Play Store"
      icon="/android.svg"
      variant="btn_dark_green_outline"
      full
    />
  </div>
  )
}

export default Getapp